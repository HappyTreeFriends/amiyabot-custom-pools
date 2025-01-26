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
                    <icon-button :icon="Upload" type="success" style="margin-left: 20px;"
                        @click="SaveOperator">
                        保存
                    </icon-button>
                </div>
            </n-form>
        </n-card>
    </n-modal>

</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import JSZip from 'jszip';
import { useRouter } from 'vue-router';
import UploadImageAsText from '@/desktop/components/UploadImageAsText.vue'
import Operator from '@/desktop/components/Operator.vue'
import EditOperator from '@/desktop/views/EditOperator.vue'
import IconButton from '@/universal/components/IconButton.vue'
import { Upload, Add, Edit, Star } from '@icon-park/vue-next'
import { getClasses, getClassImage } from '@/utils/classes'

const router = useRouter();

const poolImageBase64 = ref<string | null>('');

const uploading = ref<boolean>(false);
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
    console.log('SaveOperator',addedOperator)
}

const onUploadButtonClick = async () => {
    if (finalZipFile != null) {
        upload()
    } else {
        await calcuate()
    }
}

const upload = () => {
    const url = window.URL.createObjectURL(finalZipFile)

    // 测试用自动下载（注意：某些浏览器可能阻止非用户触发的下载）
    const link = document.createElement('a')
    link.href = url
    link.download = 'pool.zip'
    link.click()
}


const generateJson = () => {

    const getPickupRate = (level) => {

        var defaultUpRates = {
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

    const getPickup = (level) => {

        var operators = []

        operators = [...operators , ...officialOperators[level.toString()]]
        operators = [...operators , ...customOperators.value.filter(op => op.rarity == level).map(op => op.name)]

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

        version: 1
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

    const zip = new JSZip();

    const pureBase64 = poolImageBase64.value.split(',')[1] || poolImageBase64.value
    zip.file("pool_image.png", pureBase64, { base64: true })

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

    stream.on('data', (chunk: Uint8Array, metadata) => {
        chunks.push(chunk)
        totalSize += chunk.byteLength
        var totalSizeInMB = totalSize / 1024 / 1024
        var zipFileSizePrecentageValue = totalSizeInMB / 50 * 100
        if (zipFileSizePrecentageValue >= 100) {
            zipFileSizePrecentageValue = 100
            zipFileSizeStatus.value = "error"
        } else {
            zipFileSizeStatus.value = "default"
        }
        zipFileSizePrecentage.value = zipFileSizePrecentageValue
        zipFileSizeText.value = `${totalSizeInMB.toFixed(2)}MB / 50MB`
    })

    stream.on('end', () => {
        const blob = new Blob(chunks, { type: 'application/zip' })
        console.log('最终 ZIP 文件:', blob)
        uploadButtonDisabled.value = false;
        uploadButtonText.value = '上传到服务器';
        finalZipFile = blob;
    })

    // 开始生成
    stream.resume()
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
    width: 50vw;
    height: 80vh;
}
</style>