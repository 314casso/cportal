import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import { environment } from '../../environments/environment';
import { News } from '../_models/news';

@Injectable()
export class NewsService {
    private apiUrl = environment.apiUrl + 'api/news/';

    constructor(
        private http: HttpClient
    ) { }

    getNews() {
        return this.http.get<News[]>(this.apiUrl)
                        .catch((error: HttpErrorResponse) => {
                            console.error('Error response catched during News request', error);
                            return Observable.of([]);
                        });
    }
}
