import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import { environment } from '../../environments/environment';
import { Employee } from '../_models/employee';

@Injectable()
export class EmployeeService {
    private apiUrl = environment.apiUrl + 'api/employees/';

    constructor(
        private http: HttpClient
    ) { }

    getEmployees() {
        return this.http.get<Employee[]>(this.apiUrl)
                        .catch((error: HttpErrorResponse) => {
                            console.error('Error response catched during Employee request', error);
                            return Observable.of([]);
                        });
    }
}
