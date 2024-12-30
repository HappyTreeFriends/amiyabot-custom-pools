<template>
    <div class="uploader-body">
        <n-upload @before-upload="beforeUpload" class="n-uploader">
            <n-upload-dragger class="upload-dragger">
                <div class="icon-container">
                    <n-icon size="40" :depth="3">
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
    </div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef, onMounted } from 'vue';
import { UploadPicture } from '@icon-park/vue-next'
import { UploadFileInfo } from 'naive-ui';
import { Close } from '@icon-park/vue-next';

const model = defineModel<string | null>({ required: true })

defineProps<{
    text: string;
}>();

const displayMask = ref(false);

const imageMask = useTemplateRef('imageMask')

onMounted(() => {
    // 从model中获取图片的base64编码，并将其填入
    if (model.value) {
        displayMask.value = true;
        const img = imageMask.value as HTMLImageElement;
        img.src = model.value;
    }
})

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
        displayMask.value = true;

        const img = imageMask.value as HTMLImageElement;
        img.src = base64Str;

        model.value = base64Str;
        console.log("Image Loaded.");
    };
    reader.readAsDataURL(blob);

    return false;
};

</script>

<style scoped lang="scss">
.uploader-body {
    position: relative;
    display: block;
}

.n-uploader {
    width: 100%;
    height: 100%;
}

.upload-dragger {
    display: flex;
    flex-direction: column;
}

.icon-container {
    margin-bottom: 12px;
    display: flex;
    justify-content: center;
}

.main-text {
    font-size: 20px;
}

.sub-text {
    font-size: 16px;
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
</style>