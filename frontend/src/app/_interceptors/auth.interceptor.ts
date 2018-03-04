import { Injectable} from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let token: string;
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (currentUser && currentUser.token) {
            token = currentUser.token;
        }
        if (token) {
            const cloned = req.clone({ headers: req.headers.set('Authorization', 'JWT ' + token) });
            return next.handle(cloned);
        } else {
            return next.handle(req);
        }
    }
}
