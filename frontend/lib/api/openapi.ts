/**
 * FastAPI
 * 0.1.0
 * DO NOT MODIFY - This file has been generated using oazapfts.
 * See https://www.npmjs.com/package/oazapfts
 */
import * as Oazapfts from "@oazapfts/runtime";
import * as QS from "@oazapfts/runtime/query";
export const defaults: Oazapfts.Defaults<Oazapfts.CustomHeaders> = {
    headers: {},
    baseUrl: "/",
};
const oazapfts = Oazapfts.runtime(defaults);
export const servers = {};
export type ValidationError = {
    loc: (string | number)[];
    msg: string;
    "type": string;
};
export type HttpValidationError = {
    detail?: ValidationError[];
};
export type GetAssetMetadataResponse = {
    content_type: string;
    alt?: string | null;
};
export type BodyUploadAssetApiAssetsPost = {
    file: Blob;
    alt?: string | null;
};
export type UploadFileResponse = {
    hash: string;
    content_type: string;
    alt?: string | null;
};
export type UserResponse = {
    id: number;
    email: string;
    avatar_hash: string | null;
    display_name: string | null;
};
export type UpdateUserRequest = {
    email: string | null;
    password: string | null;
    avatar_hash?: string | null;
    display_name?: string | null;
};
export type LoginRequest = {
    email: string;
    password: string;
};
export type Session = {
    token: string;
    user_id: number | null;
    expires_at?: string;
};
export type RegisterRequest = {
    email: string;
    password: string;
};
/**
 * Get Asset
 */
export function getAsset(assetHash: string, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: Blob;
    } | {
        status: 422;
        data: HttpValidationError;
    }>(`/api/assets/${encodeURIComponent(assetHash)}`, {
        ...opts
    }));
}
/**
 * Get Asset Metadata
 */
export function getAssetMetadata(assetHash: string, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: GetAssetMetadataResponse;
    } | {
        status: 422;
        data: HttpValidationError;
    }>(`/api/assets/${encodeURIComponent(assetHash)}/metadata`, {
        ...opts
    }));
}
/**
 * Upload Asset
 */
export function uploadAsset(bodyUploadAssetApiAssetsPost: BodyUploadAssetApiAssetsPost, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: UploadFileResponse;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/assets", oazapfts.multipart({
        ...opts,
        method: "POST",
        body: bodyUploadAssetApiAssetsPost
    })));
}
/**
 * Get Self
 */
export function getSelf(opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: UserResponse;
    }>("/api/users/me", {
        ...opts
    }));
}
/**
 * Update Self
 */
export function updateSelf(updateUserRequest: UpdateUserRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: UserResponse;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/users/me", oazapfts.json({
        ...opts,
        method: "PATCH",
        body: updateUserRequest
    })));
}
/**
 * Login
 */
export function login(loginRequest: LoginRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: Session;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/login", oazapfts.json({
        ...opts,
        method: "POST",
        body: loginRequest
    })));
}
/**
 * Register
 */
export function register(registerRequest: RegisterRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: Session;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/register", oazapfts.json({
        ...opts,
        method: "POST",
        body: registerRequest
    })));
}
