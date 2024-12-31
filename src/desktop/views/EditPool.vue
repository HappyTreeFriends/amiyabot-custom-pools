<template>
    <UploadImageAsText text="上传卡池头图"
    :aspect-ratio="16 / 9"
    v-model="imageBase64"/>
    <router-link to="/edit-pool/edit-operator">编辑操作员</router-link>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import UploadImageAsText from '@/desktop/components/UploadImageAsText.vue'

const imageBase64 = ref<string | null>('');

</script>

<style scoped lang="scss">
.login {
    width: 100%;
    height: 100%;
    background: url(../../assets/bg.svg) center / cover no-repeat;
    display: flex;
    flex-direction: column;
    align-items: center;

    .main-body {
        display: flex;
        flex: 2;
        flex-direction: column;
        align-items: center;
        padding-top: 40px;
        width: 50%;

        .title {
            font-size: 34px;
            margin-bottom: 50px;
        }
    }

    .footer {
        text-align: center;
        font-size: 14px;
        color: gray;
        padding-bottom: 10px;

        & > div:first-child {
            margin-bottom: 5px;
        }

        & > div:last-child {
            display: flex;
            justify-content: center;
            height: 16px;
        }

        .friendly-link {
            display: flex;
            align-items: center;
            margin: 0 3px;
            text-align: center;
            text-decoration: none;
            color: gray;
            font-size: 12px;
        }
    }
}
</style>