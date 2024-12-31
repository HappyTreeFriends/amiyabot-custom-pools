<template>
    <div class="login">
        <div class="main-body">
            <n-breadcrumb separator=">">
                <n-breadcrumb-item v-for="(item, index) in breadcrumbItems" :key="index">
                    <router-link :to="item.link">{{ item.text }}</router-link>
                </n-breadcrumb-item>
            </n-breadcrumb>
            <n-card>
                <router-view />
            </n-card>
        </div>
        <div class="footer">
            <div>本网站不是鹰角网络官方网站，而是由爱好者自行开发的工具网站。</div>
            <div>
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo"
                    width="12" height="12" />
                <a class="friendly-link" href="https://github.com/hsyhhssyy/amiyabot-minigame-center-website"
                    target="_blank">
                    GitHub Repository
                </a>
                <n-divider vertical />
                <img src="https://img.alicdn.com/tfs/TB1..50QpXXXXX7XpXXXXXXXXXX-40-40.png" alt="Beian Logo" width="12"
                    height="12" />
                <a class="friendly-link" href="https://beian.miit.gov.cn/" target="_blank"> 京ICP备2022033983-2号 </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, watch } from 'vue';
import { useRoute, onBeforeRouteUpdate } from 'vue-router';

const breadcrumbItems :any = ref([]);
const route = useRoute();

const updateBreadcrumb = (route:any) => {
  if (route.name === 'edit-operator') {
    breadcrumbItems.value = [
      { text: '卡池编辑', link: '/edit-pool' },
      { text: '干员编辑', link: '' }
    ];
  } else {
    breadcrumbItems.value = [
      { text: '卡池编辑', link: '' }
    ];
  }
};

// 初始化面包屑
updateBreadcrumb(route);

// 监听路由变化
onBeforeRouteUpdate((to, from, next) => {
  updateBreadcrumb(to);
  next();
});

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

        &>div:first-child {
            margin-bottom: 5px;
        }

        &>div:last-child {
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