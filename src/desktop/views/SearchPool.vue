<template>
    <n-card class="room-list" embedded>
        <div class="room-list-body">
            <n-space justify="space-between" style="padding: 0 5px">
                <n-space>
                    <icon-button :icon="Refresh" type="info">刷新卡池列表</icon-button>
                    <icon-button :icon="Back" type="error">返回</icon-button>
                </n-space>
                <n-input-group>
                    <n-input placeholder="输入关键字以搜索" />
                    <icon-button :icon="Search" type="primary">搜索卡池</icon-button>
                </n-input-group>
            </n-space>
            <div class="room-list-content">
                <div class="room-item" v-for="(_, index) in currList" :key="index">
                    <n-card size="small" hoverable @click="openPreview = true">
                        <n-space justify="space-between">
                            <img class="game-logo" alt="" src="/demo/pool-image.png" />
                        </n-space>
                        <div class="room-info">
                            <div class="info-item creator">
                                <icon :icon="IdCardH" />

                                {{ "酒在饮中" }}
                            </div>
                            <div class="info-item">
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                界徐盛
                            </div>
                            <div class="info-item">
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                界徐盛
                            </div>
                            <div class="info-item">
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                <icon :icon="Star" />
                                界徐盛
                            </div>
                            <div class="info-item">
                                ... 等3位干员
                            </div>
                        </div>
                    </n-card>
                </div>
            </div>
            <div>
                <n-pagination v-model:page="currPage" :page-count="pageCount" />
            </div>
        </div>
    </n-card>
    <n-modal v-model:show="openPreview">
        <n-card class="preview-dialog" title="趣味卡池:就在引种" :bordered="false" role="dialog" aria-modal="true">
            <n-space class="dialog-panel-head" justify="space-evenly">
                <n-alert title="完整名称" type="default">
                    <n-space justify="center" class="dialog-panel-outer">
                        <icon :icon="IdCardH" />
                        <n-code :code="'酒在饮中'" language="javascript"/>
                        <button>复制到剪贴板</button>
                    </n-space>
                </n-alert>
                <n-alert title="Info 类型" type="info">
                    <p>你可以发送 <strong>兔兔切换趣味卡池 就在引种#1234</strong> 到阿米娅机器人来查看这个卡池</p>
                </n-alert>
            </n-space>
            <n-space justify="space-between">
                <img class="pool-image" alt="" src="/demo/pool-image.png" />
            </n-space>
            <div class="operator-item">
                <div v-for="(_, index) in currList" :key="index">
                    <div>
                        <img class="operator-logo" alt="" src="/demo/xusheng-portait.png" />
                        <div class="operator-star">

                            <icon :icon="Star" />
                            <icon :icon="Star" />
                            <icon :icon="Star" />
                            <icon :icon="Star" />
                            <icon :icon="Star" />
                            <icon :icon="Star" />
                        </div>
                        <div class="operator-name">
                            界徐盛
                        </div>
                    </div>
                </div>
            </div>
        </n-card>
    </n-modal>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Back, Star, IdCardH, Refresh, Search } from '@icon-park/vue-next'
import IconButton from '@/universal/components/IconButton.vue'
import Icon from '@/universal/components/Icon.vue'

const currList = ref(["", ""])
const currPage = ref(1)
const pageCount = ref(1)

const openPreview = ref(false)

</script>

<style lang="scss" scoped>
.room-list {
    height: 100%;

    .room-list-body {
        height: 100%;
        display: flex;
        flex-direction: column;

        .room-list-content {
            height: calc(100% - 34px - 28px - 20px);
            margin: 10px 0;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            overflow: auto;

            .room-item {
                width: min(240px, calc(100% / 4));
                padding: 5px;

                .game-logo {
                    width: 200px;
                    border-radius: 4px;
                }

                .info-item {
                    display: flex;
                    ;
                    align-items: center;
                }
            }
        }
    }
}


.preview-dialog {
    width: 80vw;
    height: 80vh;


    .dialog-panel-head {
        width: 100%;

        .dialog-panel-outer{
        user-select: text;
        cursor: text;

        .dialog-panel-selectable {
            user-select: text;
        }
        }

    }

    .pool-image {
        height: min(20vh, 200px);
        border-radius: 4px;
    }

    .operator-item {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;

        .operator-logo {
            height: 200px;
            border-radius: 4px;
        }

        .operator-star {
            display: flex;
            flex-direction: horizontal;
        }

        .operator-name {
            display: flex;
            flex-direction: horizontal;
            align-items: center;
            align-self: center;
        }
    }
}
</style>
