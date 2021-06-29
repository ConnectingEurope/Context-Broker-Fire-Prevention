export interface Entity {
    id?: string;
    type?: string;
    location?: any;
    fireWeatherIndex?: any;
    dailySeverityRating?: any;
    smokeDetected?: boolean;
    smokeDetectedConfidence?: number;
    dryDetected?:boolean;
    greenLeaves?: number;
    dryLeaves?: number;
}
