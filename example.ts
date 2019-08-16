export interface Root {
    x: GenericEdge;
}

export interface GenericEdge {
    cose: X;
}

export interface X {
    x: string;
}

export interface A {
    x: string;
}

export interface B {
    x: string;
}

export interface C {
    x: string;
}

export interface D {
    x: string;
}

export interface E {
    x: string;
}

export interface Object {
    aCiao?: number;
    bCom:   string;
    sdf?:   number;
}

/**
 * Descrizione Campaign
 *
 *
 *
 * Descrizione PostCampaign
 *
 * Descrizione Node
 *
 * Descrizione MessageCampaign
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
     * Descrizione x
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
     * Descrizione x
     */
    x: number;
}

/**
 * Descrizione MessageCampaign
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
