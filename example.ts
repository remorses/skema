export interface Object {
    aCiao?: number;
    bCom:   string;
    sdf?:   number;
}

/**
 * Descrizione PostCampaign
 *
 * Descrizione Node
 *
 * Descrizione della camp
 *
 * Descrizione MessageOwn
 */
export interface Campaign {
    label: string;
    y:     number;
    /**
     * Descrizione name
     */
    name:   string;
    posts?: Posts[];
    /**
     * Descrizione della prop
     */
    x?: number;
}

export interface Posts {
    name: string;
    url:  string;
}

export interface Base {
    label: string;
    y:     number;
}

/**
 * Descrizione Node
 */
export interface Node {
    /**
     * Descrizione name
     */
    name: string;
}

/**
 * Descrizione PostCampaign
 *
 * Descrizione Node
 */
export interface PostCampaign {
    label: string;
    y:     number;
    /**
     * Descrizione name
     */
    name:  string;
    posts: Posts[];
    /**
     * Descrizione della prop
     */
    x: number;
}

/**
 * Descrizione della camp
 *
 * Descrizione MessageOwn
 */
export interface MessageCampaign {
    label: string;
    y:     number;
    name:  string;
}

/**
 * Descrizione MessageOwn
 */
export interface MessageOwn {
    name: string;
}
