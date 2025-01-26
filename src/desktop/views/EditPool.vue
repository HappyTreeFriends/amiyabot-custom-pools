<template>
    <n-form label-width="auto" label-placement="left">
        <n-form-item label="卡池名称：">
            <n-input v-model:value="poolName" placeholder="卡池名称" />
        </n-form-item>
        <UploadImageAsText text="上传卡池头图" v-model="poolImageBase64" />
        <n-collapse>
            <n-collapse-item title="高级设置" style="margin: 10px;">
                <div>
                    <n-form-item label="卡池描述：">
                        <n-input v-model:value="poolDescription" placeholder="卡池描述" type="textarea" :autosize="{
                            minRows: 3,
                            maxRows: 5,
                        }" />
                    </n-form-item>
                    <n-form-item label="只出现UP角色">
                        <n-switch v-model:value="onlyUpOperators" />
                    </n-form-item>
                    <n-form label-placement="left" :disabled="onlyUpOperators">
                        <n-grid :cols="2">
                            <n-form-item-gi :label="star + '星UP出率(%)：'" v-for="star in [6, 5, 4, 3, 2, 1]" :key="star">
                                <n-input-number :placeholder="star + '星UP出率(%)：'"
                                    v-model:value="upRates[star.toString()]" />
                            </n-form-item-gi>
                        </n-grid>
                    </n-form>
                </div>
            </n-collapse-item>
        </n-collapse>
        <n-collapse>
            <n-collapse-item title="添加自定义UP干员" style="margin: 10px;">
                <div class="custom-operators">
                    <div v-for="op in customOperators" :key="op">
                        <operator @click="editOperator(op)" :operatorData="op"></operator>
                    </div>
                    <n-button type="tertiary" size="large" @click="newOperator" class="operator-add">
                        <n-icon :component="Add" />
                    </n-button>
                </div>
            </n-collapse-item>
        </n-collapse>
        <n-collapse>
            <n-collapse-item title="添加官方UP干员" style="margin: 10px;">
                <div v-for="star in [6, 5, 4, 3, 2, 1]" :key="star">
                    <n-form-item :label="'官方' + star + '星干员'">
                        <n-dynamic-tags v-model:value="officialOperators[star.toString()]" />
                    </n-form-item>
                </div>
            </n-collapse-item>
        </n-collapse>
        <div class="form-buttons">
            <icon-button :icon="Upload" type="success" :disabled="uploadButtonDisabled" @click="onUploadButtonClick">
                {{ uploadButtonText }}
            </icon-button>
            <n-progress type="line" :height="24" :percentage="zipFileSizePrecentage" :status="zipFileSizeStatus"
                style="margin-left: 20px;">
                {{ zipFileSizeText }}
            </n-progress>
        </div>
    </n-form>

    <n-modal v-model:show="editorOpen">
        <n-card style="max-width: 80%; width: fit-content;">
            <n-form class="operator-form" label-placement="left" :label-width="80">
                <n-form-item label="干员名：">
                    <n-input type="text" id="name" v-model:value="editingOperatorName" placeholder="输入干员名称"
                        :disabled="editingOperatorNameReadOnly" />
                </n-form-item>

                <n-form-item label="稀有度：">
                    <n-rate v-model:value="editingOperatorRarity" :count="6" size="large" />
                </n-form-item>

                <n-form-item label="职业：">
                    <n-radio-group v-model:value="editingOperatorClass">
                        <n-radio v-for="(classChinese, className) in getClasses()" :key="className" :value="className"
                            :label="classChinese">
                        </n-radio>
                    </n-radio-group>
                </n-form-item>

                <n-form label-placement="left">
                    <n-grid :cols="2">
                        <n-form-item-gi label="干员全身照">
                            <UploadImageAsText class="portrait-upload" text="" :aspect-ratio="1 / 2"
                                v-model="editingOperatorPortrait" />
                        </n-form-item-gi>
                        <n-form-item-gi label="干员头像">
                            <UploadImageAsText class="avatar-upload" text="" :aspect-ratio="1 / 1"
                                v-model="editingOperatorAvatar" />
                        </n-form-item-gi>
                    </n-grid>
                </n-form>
                <div class="operator-form-buttons">
                    <icon-button :icon="Upload" type="default" @click="editorOpen = false">
                        取消
                    </icon-button>
                    <icon-button :icon="Upload" type="success" style="margin-left: 20px;" @click="SaveOperator">
                        保存
                    </icon-button>
                </div>
            </n-form>
        </n-card>
    </n-modal>

    <n-modal v-model:show="zipFileUploadResult" :mask-closable="false">
        <n-card class="uploading-dialog allow-copy" title="上传成功">
            <n-space vertical :size="10">
                <n-alert title="卡池编号" type="default">
                    <template #icon>
                        <n-icon :component="Upload" />
                    </template>
                    <n-space justify="center">
                        <n-text strong>
                            {{ zipFileUploadResult?.pool_uuid }}
                            <n-button text type="primary" :focusable="false">
                                <template #icon>
                                    <n-icon :component="Copy" />
                                </template>
                            </n-button>
                        </n-text>
                    </n-space>
                </n-alert>
                <n-alert title="完整名称" type="default">
                    <template #icon>
                        <n-icon :component="Alarm" />
                    </template>
                    <n-space justify="center">
                        <n-text strong>
                            {{ zipFileUploadResult?.unique_name }}
                            <n-button text type="primary" :focusable="false">
                                <template #icon>
                                    <n-icon :component="Copy" />
                                </template>
                            </n-button>
                        </n-text>
                    </n-space>
                </n-alert>
                <n-alert title="安全提示" type="info">
                    <template #icon>
                        <n-icon :component="Lock" />
                    </template>

                    <n-space vertical :size="12" style="align-items: center;">
                        <n-text strong depth="3">
                            {{ zipFileUploadResult?.edit_uuid }}
                            <n-button text type="primary" :focusable="false">
                                <template #icon>
                                    <n-icon :component="Copy" />
                                </template>
                            </n-button>
                        </n-text>

                        <n-text depth="3" type="error" style="font-size: 12px;">
                            重要提示：未来修改该卡池时，需要您提供该秘钥，遗失无法找回，请妥善保管秘钥。
                        </n-text>
                    </n-space>
                </n-alert>
            </n-space>
            <template #footer>
        <div style="width: 100%; display: flex; justify-content: center;">
          <n-button type="primary" @click="closeUploadResult">确定</n-button>
        </div>
      </template>
        </n-card>
    </n-modal>

</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import JSZip from 'jszip';
import UploadImageAsText from '@/desktop/components/UploadImageAsText.vue'
import Operator from '@/desktop/components/Operator.vue'
import IconButton from '@/universal/components/IconButton.vue'
import { Upload, Add, Lock, Alarm, Copy } from '@icon-park/vue-next'
import { getClasses } from '@/utils/classes'
import { uploadZip,UploadZipResponse } from '@/utils/server'

const poolImageBase64 = ref<string | null>('');

const uploadButtonDisabled = ref<boolean>(false);
const uploadButtonText = ref<string>('计算文件大小');

const poolName = ref<string>('');
const poolDescription = ref<string>('');

const customOperators = ref<any[]>([]);

const onlyUpOperators = ref<boolean>(false);

const upRates = reactive<Record<string, number>>({
    '6': 70,
    '5': 50,
    '4': 0,
    '3': 0,
    '2': 0,
    '1': 0
});

const officialOperators = reactive<Record<string, string[]>>({
    '6': [],
    '5': [],
    '4': [],
    '3': [],
    '2': [],
    '1': []
});

const editingOperatorName = ref<string>('');
const editingOperatorNameReadOnly = ref<boolean>(false);
const editingOperatorRarity = ref<number>(6);
const editingOperatorPortrait = ref<string>('');
const editingOperatorAvatar = ref<string>('');
const editingOperatorClass = ref<string>('');

const editorOpen = ref<boolean>(false);

const zipFileSizePrecentage = ref<number>(0);
const zipFileSizeText = ref<string>("0MB / 50MB");
const zipFileSizeStatus = ref<string>("default");

var finalZipFile: Blob | null = null;

const zipFileUploadResult = ref<UploadZipResponse|null>();

const editOperator = (op: any) => {
    console.log(op);
    editingOperatorName.value = op.name;
    editingOperatorNameReadOnly.value = true;
    editingOperatorClass.value = op.class;
    editingOperatorRarity.value = op.rarity;
    editingOperatorPortrait.value = op.portrait;
    editingOperatorAvatar.value = op.avatar;

    editorOpen.value = true;
}

const newOperator = () => {
    editingOperatorName.value = '';
    editingOperatorNameReadOnly.value = false;
    editingOperatorRarity.value = 6;
    editingOperatorPortrait.value = '';
    editingOperatorAvatar.value = '';
    editingOperatorClass.value = '';
    editorOpen.value = true;
}

const SaveOperator = () => {
    var addedOperator = {
        name: editingOperatorName.value,
        rarity: editingOperatorRarity.value,
        portrait: editingOperatorPortrait.value,
        avatar: editingOperatorAvatar.value,
        class: editingOperatorClass.value
    }
    customOperators.value.push(addedOperator)
    editorOpen.value = false;
    console.log('SaveOperator', addedOperator)
}

const onUploadButtonClick = async () => {
    if (finalZipFile != null) {
        await upload()
    } else {
        await calcuate()
    }
}

const upload = async () => {
    if (finalZipFile == null) {
        return
    }

    uploadButtonDisabled.value = true;

    const file = new File([finalZipFile], "pool.zip", {
        type: 'application/zip',
        lastModified: Date.now()
    });

    var resp = await uploadZip(file)
    // const url = window.URL.createObjectURL(finalZipFile)
    // // 测试用自动下载（注意：某些浏览器可能阻止非用户触发的下载）
    // const link = document.createElement('a')
    // link.href = url
    // link.download = 'pool.zip'
    // link.click()
    if(resp.success){
        zipFileUploadResult.value = resp
    }else{        
        uploadButtonDisabled.value = false;
    }


}


const generateJson = () => {

    const getPickupRate = (level: number) => {

        var defaultUpRates: Record<string, number> = {
            '6': 70,
            '5': 50,
            '4': 0,
            '3': 0,
            '2': 0,
            '1': 0
        }

        if (onlyUpOperators.value) {
            return defaultUpRates[level.toString()]
        } else {
            return upRates[level.toString()]
        }

    }

    const getPickup = (level: number) => {

        var operators: string[] = []

        operators = [...operators, ...officialOperators[level.toString()]]
        operators = [...operators, ...customOperators.value.filter(op => op.rarity == level).map(op => op.name)]

        return operators
    }

    return {
        pool_name: poolName.value,
        pool_description: poolDescription.value,

        is_official: false,
        is_classicOnly: false,

        pickup_6: getPickup(6),
        pickup_6_rate: getPickupRate(5),
        pickup_5: getPickup(5),
        pickup_5_rate: getPickupRate(5),
        pickup_4: getPickup(4),
        pickup_4_rate: getPickupRate(4),
        pickup_3: getPickup(3),
        pickup_3_rate: getPickupRate(3),
        pickup_2: getPickup(2),
        pickup_2_rate: getPickupRate(2),
        pickup_1: getPickup(1),
        pickup_1_rate: getPickupRate(1),

        version: 1,
        custom_operators: [] as Array<{ name: string; rarity: number; class: string; avatar: string; portrait: string }>
    }
}

const generateUuid = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

const calcuate = async () => {
    uploadButtonDisabled.value = true;
    uploadButtonText.value = '计算中......';

    const startTime = Date.now();
    const zip = new JSZip();

    if (poolImageBase64.value != null) {
        const pureBase64 = poolImageBase64.value.split(',')[1] || poolImageBase64.value
        zip.file("pool_image.png", pureBase64, { base64: true })
    }

    var customOperatorsJsonPayload = []

    for (const op of customOperators.value) {
        if (op.uuid == null) {
            op.uuid = generateUuid()
        }
        const avatarBase64 = op.avatar.split(',')[1] || op.avatar
        const portraitBase64 = op.portrait.split(',')[1] || op.portrait
        zip.file(`operators/${op.uuid}.avatar.png`, avatarBase64, { base64: true })
        zip.file(`operators/${op.uuid}.portrait.png`, portraitBase64, { base64: true })

        customOperatorsJsonPayload.push({
            name: op.name,
            rarity: op.rarity,
            class: op.class,
            avatar: `operators/${op.uuid}.avatar.png`,
            portrait: `operators/${op.uuid}.portrait.png`
        })
    }

    var poolJson = generateJson()

    poolJson.custom_operators = customOperatorsJsonPayload

    zip.file("meta-data.json", JSON.stringify(poolJson));

    const stream = zip.generateInternalStream({
        type: 'uint8array',
        compression: 'DEFLATE',
        streamFiles: true
    })

    const chunks: Uint8Array[] = []

    let totalSize = 0

    stream.on('data', (chunk: Uint8Array, _) => {
        chunks.push(chunk)
        totalSize += chunk.byteLength
        var totalSizeInMB = totalSize / 1024 / 1024
        var zipFileSizePrecentageValue = totalSizeInMB / 50 * 100
        if (zipFileSizePrecentageValue >= 100) {
            zipFileSizePrecentageValue = 100
            zipFileSizeStatus.value = "error"
        } else {
            if (zipFileSizePrecentageValue <= 0.01) {
                totalSizeInMB = 0.01
            }
            zipFileSizeStatus.value = "default"
        }
        zipFileSizePrecentage.value = zipFileSizePrecentageValue
        zipFileSizeText.value = `${totalSizeInMB.toFixed(2)}MB / 50MB`
    })

    stream.on('end', () => {
        // 计算已用时间并补足剩余时间（至少等待 1 秒）
        const elapsedTime = Date.now() - startTime;
        const remainingDelay = Math.max(1000 - elapsedTime, 0);

        setTimeout(() => {
            const blob = new Blob(chunks, { type: 'application/zip' })
            console.log('最终 ZIP 文件:', blob)
            uploadButtonDisabled.value = false;
            uploadButtonText.value = '上传到服务器';
            finalZipFile = blob;
        }, remainingDelay); // 剩余延迟补足到 1 秒
    })

    // 开始生成
    stream.resume()
}

const closeUploadResult = () => {
    zipFileUploadResult.value = null
    finalZipFile = null
    uploadButtonText.value = '计算文件大小'
    zipFileSizePrecentage.value = 0    
    uploadButtonDisabled.value = false;
}

</script>

<style scoped lang="scss">
.custom-operators {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;

    .operator-add {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 110px;
        height: 50px;
        margin-left: 2.5px;
    }
}

.form-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.avatar-upload {
    height: 120px;
    width: 120px;
    font-size: 10px;
}


.portrait-upload {
    height: 240px;
    width: 120px;
}

.operator-editor-class-icon {
    height: 25px;
    width: 25px;
}

.uploading-dialog {
    width: 500px;
    gap: 10px;
}

.allow-copy,
.allow-copy *,
.allow-copy *::before,
.allow-copy *::after {
    user-select: text;
}
</style>