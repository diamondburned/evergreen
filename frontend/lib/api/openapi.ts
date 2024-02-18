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
    id: string;
    email: string | null;
    avatar_hash: string | null;
    display_name: string | null;
};
export type UpdateUserRequest = {
    email?: string | null;
    password?: string | null;
    avatar_hash?: string | null;
    display_name?: string | null;
};
export type SessionResponse = {
    token: string;
    user_id: string;
    expires_at: string;
    is_anonymous: boolean;
};
export type RegisterSessionRequest = {
    email: string;
    password: string;
    display_name: string;
};
export type LoginSessionRequest = {
    email: string;
    password: string;
};
export type RoundInfo = {
    score: number;
    revealed_answer: boolean;
};
export type ScoreSubmission = {
    id?: number | null;
    game_category: string;
    game_difficulty: GameDifficulty;
    user_id: string;
    rounds: RoundInfo[];
    average_score: number;
    time_taken: number;
    submitted_at?: string;
};
export type SubmitScoreRequest = {
    game_category: string;
    game_difficulty: GameDifficulty;
    rounds: RoundInfo[];
    average_score: number;
    time_taken: number;
};
export type SubmitScoreResponse = {
    id: number;
    game_category: string;
    game_difficulty: GameDifficulty;
    rounds: RoundInfo[];
    average_score: number;
    time_taken: number;
    submitted_at: string;
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
 * Create Session
 */
export function createSession(opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: SessionResponse;
    }>("/api/sessions", {
        ...opts,
        method: "POST"
    }));
}
/**
 * Register Session
 */
export function registerSession(registerSessionRequest: RegisterSessionRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: any;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/sessions/register", oazapfts.json({
        ...opts,
        method: "POST",
        body: registerSessionRequest
    })));
}
/**
 * Login
 */
export function login(loginSessionRequest: LoginSessionRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: SessionResponse;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/login", oazapfts.json({
        ...opts,
        method: "POST",
        body: loginSessionRequest
    })));
}
/**
 * List Scores
 */
export function listScores({ gameCategory, gameDifficulty, fromTime, toTime }: {
    gameCategory?: string | null;
    gameDifficulty?: GameDifficulty | null;
    fromTime?: string | null;
    toTime?: string | null;
} = {}, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: ScoreSubmission[];
    } | {
        status: 422;
        data: HttpValidationError;
    }>(`/api/scores${QS.query(QS.explode({
        game_category: gameCategory,
        game_difficulty: gameDifficulty,
        from_time: fromTime,
        to_time: toTime
    }))}`, {
        ...opts
    }));
}
/**
 * Submit Score
 */
export function submitScore(submitScoreRequest: SubmitScoreRequest, opts?: Oazapfts.RequestOpts) {
    return oazapfts.ok(oazapfts.fetchJson<{
        status: 200;
        data: SubmitScoreResponse;
    } | {
        status: 422;
        data: HttpValidationError;
    }>("/api/scores", oazapfts.json({
        ...opts,
        method: "POST",
        body: submitScoreRequest
    })));
}
export enum GameDifficulty {
    Beginner = "beginner",
    Intermediate = "intermediate",
    Advanced = "advanced"
}
