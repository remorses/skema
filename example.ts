/**
 * ciao
 */
export interface Example {
    a_come_stai?: number;
    /**
     * ciao
     */
    bCiaoComeVa?: BoCiao;
}

/**
 * ciao
 */
export interface BoCiao {
    ciaoComeVa?: number;
    enum?:       Enum;
    xxx?:        Xxx;
}

export enum Enum {
    CiaoComeVa = "ciaoComeVa",
    SdfAdf = "sdf_adf",
}

/**
 * ciao
 */
export interface Xxx {
    sd?: number;
    zz:  number;
}
