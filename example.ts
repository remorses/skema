export interface Object {
    aCiao?: number;
    bCom:   string;
    sdf?:   number;
}

export interface Campaign {
    label:  string;
    x:      number;
    y:      number;
    name:   string;
    posts?: Posts[];
}

export interface Posts {
    name: string;
    url:  string;
}

export interface Base {
    label: string;
    x:     number;
    y:     number;
}

export interface Node {
    name: string;
}

export interface PostCampaign {
    label: string;
    x:     number;
    y:     number;
    name:  string;
    posts: Posts[];
}

export interface MessageCampaign {
    label: string;
    x:     number;
    y:     number;
    name:  string;
}

export interface MessageOwn {
    name: string;
}
