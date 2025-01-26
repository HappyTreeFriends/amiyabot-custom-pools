<template>
    <div class="uploader-body">
        <n-upload @before-upload="beforeUpload" class="n-uploader" :abstract="false">
            <n-upload-dragger class="upload-dragger">
                <div class="icon-container">
                    <n-icon size="30" :depth="3">
                        <UploadPicture />
                    </n-icon>
                </div>
                <n-text class="main-text">
                    {{ text }}
                </n-text>
                <n-text class="sub-text">
                    点击或者拖动图片文件到该区域
                </n-text>
            </n-upload-dragger>
        </n-upload>
        <div class="image-mask" v-show="displayMask">
            <img class="image-mask-img" ref="imageMask" alt="Uploaded Image" />
        </div>
        <n-button class="image-mask-close-button" quaternary circle type="error" @click="removeImage"
            v-show="displayMask">
            <Close />
        </n-button>
        <n-modal v-model:show="cropperOpen" :close-on-click-modal="false" :close-on-press-escape="false"
            @after-enter="dialogOpen">
            <n-card class="cropper-dialog" title="调整大小" :bordered="false" role="dialog" aria-modal="true">
                <div class="cropper-dialog-card-content">
                    <div class="cropper-div">
                        <img ref="imageCropper" class="cropper-img" id="image" :src="'' + intermidiateImageBase64">
                    </div>
                    <div class="cropper-dialog-button-bar">
                        <n-button type="error" @click="cropperOpen = false">取消</n-button>
                        <n-button type="primary" @click="dialogClose">确定</n-button>
                    </div>
                </div>
            </n-card>
        </n-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, onMounted } from 'vue';
import { UploadPicture } from '@icon-park/vue-next'
import { UploadFileInfo } from 'naive-ui';
import { Close } from '@icon-park/vue-next';

import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';

const model = defineModel<string | null>({ required: true })

const prop = defineProps<{
    text: string;
    aspectRatio?: number;
}>();

const displayMask = ref(false);
const cropperOpen = ref(false);

const imageMask = useTemplateRef('imageMask')
const imageCropper = useTemplateRef('imageCropper')

const intermidiateImageBase64 = ref<string | null>(null);

var cropper: any;

onMounted(() => {
    // 从model中获取图片的base64编码，并将其填入
    if (model.value) {
        displayMask.value = true;
        const img = imageMask.value as HTMLImageElement;
        img.src = model.value;
    }

})

const dialogOpen = () => {

    const imgC = imageCropper.value as HTMLImageElement;
    var data = {}

    if (prop.aspectRatio) {
        data = {
            aspectRatio: prop.aspectRatio
        }
    }

    cropper = new Cropper(imgC, data);
}

const removeImage = () => {
    displayMask.value = false;
    model.value = null;
}

const beforeUpload = (data: {
    file: UploadFileInfo
    fileList: UploadFileInfo[]
}) => {
    const file = data.file.file!;
    const blob = new Blob([file], { type: file.type });
    const reader = new FileReader();
    reader.onloadend = () => {
        const base64Str = reader.result as string;
        intermidiateImageBase64.value = base64Str;
        cropperOpen.value = true;
    };
    reader.readAsDataURL(blob);

    return false;
};

const dialogClose = () => {
    const croppedCanvas = cropper.getCroppedCanvas();

    // 将裁剪的 Canvas 转换为 DataURL（Base64 图片）
    const croppedImageURL = croppedCanvas.toDataURL('image/png');
    //console.log(croppedImageURL);
    model.value = croppedImageURL;
    //console.log("Image Loaded.");
    cropperOpen.value = false;


    const img = imageMask.value as HTMLImageElement;
    img.src = croppedImageURL;
    displayMask.value = true;

}

</script>

<style lang="scss" scoped>
.uploader-body {
    position: relative;
    display: block;

    .n-uploader {
        width: 100%;
        height: 100%;

        .upload-dragger {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            padding: 10px;
            justify-content: center;
            /* 水平居中 */
            align-items: center;
            /* 垂直居中 */

            .icon-container {
                margin-bottom: 10px;
                display: flex;
                justify-content: center;
            }

            .main-text {
                font-size: 14px;
            }

            .sub-text {
                font-size: 12px;
            }
        }
    }

    .image-mask {
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        position: absolute;
        border: 2px dashed #000;
        background: rgba(255, 255, 255, 255);
        z-index: 10;

        .image-mask-img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    }

    .image-mask-close-button {
        position: absolute;
        top: 0;
        right: 0;
        z-index: 20;
    }


}

.cropper-dialog {
    // width 和 height都设为 80vh 和 80vw 中小的那一个
    width: min(80vh, 80vw);
    height: min(80vh, 80vw);

    .cropper-dialog-card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;

        .cropper-div {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;

            .cropper-img {
                display: block;

                /* This rule is very important, please don't ignore this */
                max-width: 100%;
            }
        }

        .cropper-dialog-button-bar {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin-top: 20px;
            margin-bottom: 40px;
        }
    }
}
</style>

<style lang="scss">
.n-upload-trigger {
    height: 100%;
    width: 100%;
}
</style>