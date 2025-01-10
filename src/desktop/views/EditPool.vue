<template>
    <n-form label-width="auto" label-placement="left">
        <n-form-item label="卡池名称：">
            <n-input v-model:value="poolName" placeholder="卡池名称" />
        </n-form-item>
        <UploadImageAsText text="上传卡池头图" v-model="imageBase64" />
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
                        <n-switch />
                    </n-form-item>
                    <n-form label-placement="left">
                        <n-grid :cols="2">
                            <n-form-item-gi label="六星UP出率(%)：">
                                <n-input-number placeholder="六星UP出率(%)" />
                            </n-form-item-gi>
                            <n-form-item-gi label="五星UP出率(%)：">
                                <n-input-number placeholder="五星UP出率(%)" />
                            </n-form-item-gi>
                            <n-form-item-gi label="四星UP出率(%)：">
                                <n-input-number placeholder="四星UP出率(%)" />
                            </n-form-item-gi>
                            <n-form-item-gi label="三星UP出率(%)：">
                                <n-input-number placeholder="三星UP出率(%)" />
                            </n-form-item-gi>
                            <n-form-item-gi label="二星UP出率(%)：">
                                <n-input-number placeholder="二星UP出率(%)" />
                            </n-form-item-gi>
                            <n-form-item-gi label="一星UP出率(%)：">
                                <n-input-number placeholder="一星UP出率(%)" />
                            </n-form-item-gi>
                        </n-grid>
                    </n-form>
                </div>
            </n-collapse-item>
        </n-collapse>
        <n-collapse>
            <n-collapse-item title="添加自定义UP干员" style="margin: 10px;">
                <div class="custom-operators">
                    <div v-for="op in operators" :key="op">
                        <operator @click="editOperator(op)"></operator>
                    </div>
                    <div class="operator-add">
                        加号
                    </div>
                </div>
            </n-collapse-item>
        </n-collapse>
        <n-collapse>
            <n-collapse-item title="添加官方UP干员" style="margin: 10px;">
                <n-dynamic-tags v-model:value="tags" />
            </n-collapse-item>
        </n-collapse>
        <div class="form-buttons">
            <icon-button :icon="Upload" type="success"
            @click="uploading = true">
                计算文件大小
            </icon-button>
            <n-progress
            type="line"
            :percentage="50"
            :height="24"
            style="margin-left: 20px;"
            >
            12MB / 50MB
            </n-progress>
        </div>
    </n-form>
    <n-modal v-model:show="uploading" :close-on-click-modal="false" :close-on-press-escape="false" :mask-closable="false">
            <n-card class="uploading-dialog" title="上传中" :bordered="false" role="dialog" aria-modal="true">
                
            </n-card>
        </n-modal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UploadImageAsText from '@/desktop/components/UploadImageAsText.vue'
import Operator from '@/desktop/components/Operator.vue'
import IconButton from '@/universal/components/IconButton.vue'
import { Upload } from '@icon-park/vue-next'

const router = useRouter();

const imageBase64 = ref<string | null>('');

const tags = ref<string[]>([]);

const uploading = ref<boolean>(false);

const poolName = ref<string>('');

const poolDescription = ref<string>('');

const operators = ref<any[]>([]);

for (let i = 0; i < 40; i++) {
    operators.value.push(i);
}

const editOperator = (op: any) => {
    console.log(op);
    // route to edit operator page
    router.push('/edit-pool/edit-operator');
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
        width: 100px;
        height: 300px;
        border: 1px solid black;
    }
}

.form-buttons{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.uploading-dialog {
    width: 50vw;
    height: 80vh;
}
</style>