import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';

import * as moment from 'moment';

import { environment } from '../../environments/environment';
import { User } from '../_models/user';
import { Token } from '../_models/token';

@Injectable()
export class AuthenticationService {
    private apiUrl = environment.apiUrl + 'api-token-auth/';
    private loggedIn = new BehaviorSubject<boolean>(false);

    get isLoggedIn() {
        // return moment().isBefore(this.getExpiration()) ? Observable.of(true) : Observable.of(false);
        return this.loggedIn.asObservable();
    }

    constructor(
        private http: HttpClient,
        private router: Router
    ) {
        // set token if saved in local storage
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (currentUser && currentUser.token) {
            this.loggedIn.next(true);
        }
    }

    login(user: User): Observable<boolean> {
        const body = { username: user.userName, password: user.password };

        return this.http.post(this.apiUrl, body)
                        .map((response: Token) => {
                            if (response) {
                                // store username and jwt token in local storage to keep user logged in between page refreshes
                                localStorage.setItem('currentUser', JSON.stringify({ userName: user.userName, token: response.token }));
                                this.loggedIn.next(true);
                                this.router.navigate(['/']);
                                // return true to indicate successful login
                                return true;
                            } else {
                                return false;
                            }
                        })
                        .catch((error: HttpErrorResponse) => {
                            console.error('Error response catched', error);
                            return Observable.of(false);
                        });
    }

    // getExpiration() {
    //     const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    //     if (currentUser && currentUser.expiration) {
    //         return moment(currentUser.expiration);
    //     }
    //     return null;
    // }

    logout() {
        // clear token remove user from local storage to log user out
        localStorage.removeItem('currentUser');

        this.loggedIn.next(false);
        this.router.navigate(['/login']);
    }
}
