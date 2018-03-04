export interface TrackResponse {
    date: string;
    type: string;
    tracks: Track[];
    files: File[];
}

interface Track {
    container: Container;
    platform: Platform;
    raildata: RailData;
    railtracking: RailTracking;
    freightdata: FreightData;
    freighttracking: FreightTracking;
}

interface Container {
    id: number;
    number: string;
    size: string;
    type: string;
    line: string;
}

interface Platform {
    id: number;
    number: string;
    foot: number;
    length: string;
    model: string;
    mtu: string;
}

interface RailData {
    id: number;
    train: string;
    invoice: number;
    departurestation: string;
    departuredate: string;
    destinationstation: string;
    totaldistance: string;
    estimatedtime: string;
}

interface RailTracking {
    id: number;
    operationstation: string;
    daysinroute: number;
    remainingdistance: string;
    arrivaldate: string;
}

class FreightData {
}

class FreightTracking {
}

interface File {
    title: string;
    file: string;
}
