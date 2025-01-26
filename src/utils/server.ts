// api.ts

export interface UploadZipResponse {
    success: boolean;
    message: string;
    unique_name?: string;
    pool_uuid?: string;
    edit_uuid?: string;
}

export interface PoolUuidResponse {
    success: boolean;
    message: string;
    pool_uuid?: string;
}

interface TopPoolsResponse {
    success: boolean;
    message: string;
    top_use_count_pools?: string[];
}

interface PoolInfo {
    uuid: string;
    unique_name: string;
    operators: string;
}

interface PaginatedResponse {
    success: boolean;
    message: string;
    data?: PoolInfo[];
    pagination?: {
        total: number;
        page: number;
        size: number;
        total_pages: number;
    };
}

// @ts-ignore
const API_BASE = window['_env_'].SERVER_ROOT

// 处理通用请求
async function fetcher<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE}${url}`, options);
    
    // 处理非成功响应
    if (!response.ok) {
        try {
            // 显式类型声明响应格式
            const errorData = await response.json();
            
            return errorData;
        } catch (jsonParseError) {
            return {
                success: false,
                message: response.statusText,
            } as T & { success: boolean; message: string };
        }
    }

    // 成功响应解析
    return response.json();
}

// 上传ZIP文件
export async function uploadZip(
    file: File,
    poolUuid?: string,
    editUuid?: string
): Promise<UploadZipResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const params = new URLSearchParams();
    if (poolUuid) params.append("pool_uuid", poolUuid);
    if (editUuid) params.append("edit_uuid", editUuid);

    return fetcher<UploadZipResponse>(`/upload-zip?${params}`, {
        method: "POST",
        body: formData,
    });
}

// 获取池UUID
export async function getPoolUuid(uniqueName: string): Promise<PoolUuidResponse> {
    return await fetcher<PoolUuidResponse>("/get-pool-uuid/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ unique_name: uniqueName }),
    });
}

// 增加使用计数
export async function incrementUseCount(poolUuid: string): Promise<void> {
    await fetcher("/increment-use-count/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pool_uuid: poolUuid }),
    });
}

// 获取热门池
export async function getTopUseCountPools(): Promise<TopPoolsResponse> {
    return await fetcher<TopPoolsResponse>("/top-use-count-pools/");
}

// 分页查询池列表
export async function listPools(
    search?: string,
    page: number = 1,
    size: number = 10
): Promise<PaginatedResponse> {
    const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
    });
    if (search) params.append("search", search);

    return fetcher<PaginatedResponse>(`/pools?${params}`);
}

// 获取池图片URL
export function getPoolImageUrl(poolUuid: string): string {
    return `${API_BASE}/pools/${poolUuid}/pool_image.png`;
}

// 获取干员头像URL
export function getOperatorAvatarUrl(
    poolUuid: string,
    operatorUuid: string
): string {
    return `${API_BASE}/pools/${poolUuid}/${operatorUuid}.avatar.png`;
}

// 获取干员立绘URL
export function getOperatorPortraitUrl(
    poolUuid: string,
    operatorUuid: string
): string {
    return `${API_BASE}/pools/${poolUuid}/${operatorUuid}.portrait.png`;
}

// 获取元数据URL
export function getMetadataUrl(poolUuid: string): string {
    return `${API_BASE}/pools/${poolUuid}/meta-data.json`;
}
