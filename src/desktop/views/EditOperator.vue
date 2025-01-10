<template>
    <n-form class="operator-form">
        <div class="operator-form-body">
            <div class="left-side">
                <n-form-item label="干员名称">
                    <n-input type="text" id="name" v-model="name" placeholder="输入干员名称" />
                </n-form-item>

                <n-form-item label="稀有度">
                    <n-radio-group class="rarity" v-model:value="rarity">
                        <n-radio-button v-for="index in 6" :key="index" :value="index">
                            <n-icon class="star-icon" size="30">
                                <star :theme="index <= rarity ? 'filled' : 'outline'" fill="#333" />
                            </n-icon>
                        </n-radio-button>
                    </n-radio-group>
                </n-form-item>
            </div>
            <div class="middle-side">
                <n-form-item label="干员全身照">
                    <UploadImageAsText class="portrait-upload" text="" :aspect-ratio="1 / 2" v-model="portrait" />
                </n-form-item>
            </div>
            <div class="right-side">
                <n-form-item label="干员头像">
                    <UploadImageAsText class="avatar-upload" text="" :aspect-ratio="1 / 1" v-model="avatar" />
                </n-form-item>
            </div>
        </div>
        <div class="operator-form-buttons">
            <icon-button :icon="Upload" type="default">
                取消
            </icon-button>
            <icon-button :icon="Upload" type="success" style="margin-left: 20px;">
                保存
            </icon-button>
        </div>
    </n-form>
</template>


<script lang="ts" setup>
import { ref } from 'vue';
import { Star, Upload } from '@icon-park/vue-next'
import IconButton from '@/universal/components/IconButton.vue'
import UploadImageAsText from '@/desktop/components/UploadImageAsText.vue'

//<star theme="two-tone" size="24" :fill="['#333' ,'#2F88FF']"/>

const name = ref<string>('');
const rarity = ref<number>(6);
const portrait = ref<string>('');
const avatar = ref<string>('');

</script>

<style lang="scss">
.operator-form {
    display: flex;
    flex-direction: column;

    .operator-form-body {
        min-height: 300px;
        display: flex;
        justify-content: space-evenly;

        .left-side {
            flex: 1;
            display: flex;
            flex-direction: column;

            .name-inputs {
                display: flex;
                align-items: center;

            }


            .rarity {
                display: flex;
                align-items: center;
            }
        }

        .middle-side {
            flex: 0.5;
            display: flex;
            margin-left: 20px;
            align-items: flex-start;

            .portrait-upload {
                height: 240px;
                width: 120px;
            }

        }

        .right-side {
            flex: 0.5;
            display: flex;
            margin-left: 20px;
            align-items: flex-start;

            .avatar-upload {
                height: 120px;
                width: 120px;
                font-size: 10px;
            }
        }
    }

    .operator-form-buttons {
        display: flex;
        justify-content: end;
    }
}
</style>