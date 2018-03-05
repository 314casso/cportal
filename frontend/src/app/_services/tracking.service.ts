import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import { environment } from '../../environments/environment';
import { TrackResponse } from '../_models/track-response';

@Injectable()
export class TrackingService {
    // private apiUrl = environment.apiUrl + 'api/trackevents/';
    private apiUrl = './assets/tracking.json';

    constructor(
        private http: HttpClient
    ) { }

    getTracks() {
        return this.http.get<TrackResponse[]>(this.apiUrl);
    }
}
