<template>
    <div class="login">
        <div class="main-body">
            <div class="title">兔兔趣味卡池站</div>
            <n-tabs type="line" animated v-model:value="tab">
                <n-tab-pane name="options" tab="options">
                    <n-space>
                        <n-card class="option-item" hoverable embedded size="small" @click="navigateTo('pick')">
                            <div class="item user">挑选趣味卡池</div>
                        </n-card>
                        <n-card class="option-item" hoverable embedded size="small" @click="navigateTo('create')">
                            <div class="item register">创建趣味卡池</div>
                        </n-card>
                        <n-card class="option-item" hoverable embedded size="small" @click="openPool = true">
                            <div class="item visitor">编辑趣味卡池</div>
                        </n-card>
                        <n-card class="option-item" hoverable embedded size="small" @click="navigateTo('bot')">
                            <div class="item bot">在QQ群里玩？</div>
                        </n-card>
                    </n-space>
                </n-tab-pane>
                <n-tab-pane name="pick" tab="pick">

                </n-tab-pane>
                <n-tab-pane name="create" tab="create">

                </n-tab-pane>
                <n-tab-pane name="edit" tab="edit">

                </n-tab-pane>
                <n-tab-pane name="bot" tab="bot">
                    <div class="commercial">
                        <div>
                            想要在QQ群里和朋友一起玩？<br />
                            点击或扫码添加阿米娅机器人到群聊。<br />
                            还有游戏数据查询等功能哦。<br />
                            <n-space style="margin-top: 20px">
                                <icon-button :icon="MessageEmoji" @click="addBotToGroup" type="primary">
                                    添加到群聊
                                </icon-button>
                                <icon-button :icon="Back" @click="goBack">返回</icon-button>
                            </n-space>
                        </div>
                        <img src="../../assets/amiyabot-qqgroup.png" alt="amiyabot" style="height: 100%" />
                    </div>
                </n-tab-pane>
            </n-tabs>
        </div>
        <div class="footer">
            <div>本网站不是鹰角网络官方网站，而是由爱好者自行开发的工具网站。</div>
            <div>
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo"
                    width="12" height="12" />
                <a class="friendly-link" href="https://github.com/HappyThreeFriends/amiyabot-custom-pools"
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
    <n-modal v-model:show="openPool" title="编辑卡池">
        <n-card class="open-pool-dialog" title="编辑卡池" :bordered="false" role="dialog" aria-modal="true">
            <n-form>
                <n-form-item label="卡池名称">
                    <n-input placeholder="卡池名称" />
                </n-form-item>
                <n-form-item label="卡池秘钥">
                    <n-input placeholder="卡池秘钥" />
                </n-form-item>
            </n-form>
            <div>
                <icon-button :icon="Back" @click="openPool = false">返回</icon-button>
            </div>
        </n-card>
    </n-modal>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Back, MessageEmoji } from '@icon-park/vue-next'
import { useRouter } from 'vue-router'
import IconButton from '@/universal/components/IconButton.vue'


const router = useRouter()

const tab = ref('options')

const openPool = ref(false)

async function goBack() {
    tab.value = 'options'
}

async function addBotToGroup() {
    window.open(
        'https://qun.qq.com/qunpro/robot/qunshare?robot_uin=2854197898&amp;robot_appid=102068219&amp;biz_type=0'
    )
}

const navigateTo = (tabIn: string) => {
    tab.value = tabIn
    switch (tabIn) {
        case 'pick':
            router.push('/search')
            break
        case 'create':
            router.push('/edit-pool')
            break
    }
}

</script>

<style scoped lang="scss">
.login {
    width: 100%;
    height: 100%;
    background: url(../../assets/bg.svg) center / cover no-repeat;
    display: flex;
    flex-direction: column;

    .main-body {
        display: flex;
        flex: 2;
        flex-direction: column;
        align-items: center;
        padding-top: 40px;

        .title {
            font-size: 34px;
            margin-bottom: 50px;
        }

        .option-item {
            cursor: pointer;

            .item {
                width: 150px;
                height: 150px;
                background: center top 0 / 80% no-repeat;
                display: flex;
                align-items: flex-end;
                justify-content: center;

                &.user {
                    background-image: url(/face/amiya/amiya_ye.webp);
                }

                &.visitor {
                    background-image: url(/face/amiya/amiya_tea.webp);
                }

                &.register {
                    background-image: url(/face/amiya/amiya_smile.webp);
                }

                &.bot {
                    background-image: url(/face/amiya/amiya_emmm.webp);
                }
            }

            &:hover {
                .item {
                    color: var(--main-color);
                }
            }
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

    .commercial {
        height: 330px;
        display: flex;
        align-items: center;
    }
}


.open-pool-dialog{
    max-width: 50vw;
    max-height: 80vh;
}

</style>
<style lang="scss">
.login {
    .main-body {
        .n-tabs-nav {
            display: none;
        }

        .n-tabs .n-tabs-pane-wrapper .n-tab-pane {
            display: flex;
            justify-content: center;
            padding: 20px 0;
        }
    }
}
</style>