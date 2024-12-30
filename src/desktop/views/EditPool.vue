<template>
    <div class="login">
        <div class="main-body">
            <UploadImageAsText text="上传卡池头图"
            v-model="imageBase64"/>
        </div>
        imageBase64: {{imageBase64}}
        <div class="footer">
            <div>本网站不是鹰角网络官方网站，而是由爱好者自行开发的工具网站。</div>
            <div>
                <img
                    src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                    alt="GitHub Logo"
                    width="12"
                    height="12"
                />
                <a
                    class="friendly-link"
                    href="https://github.com/hsyhhssyy/amiyabot-minigame-center-website"
                    target="_blank"
                >
                    GitHub Repository
                </a>
                <n-divider vertical />
                <img
                    src="https://img.alicdn.com/tfs/TB1..50QpXXXXX7XpXXXXXXXXXX-40-40.png"
                    alt="Beian Logo"
                    width="12"
                    height="12"
                />
                <a class="friendly-link" href="https://beian.miit.gov.cn/" target="_blank"> 京ICP备2022033983-2号 </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UploadPicture } from '@icon-park/vue-next'
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