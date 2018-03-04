import { Injectable } from '@angular/core';
import { MatSidenav } from '@angular/material';

import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class SidenavService {
    private sidenav: MatSidenav;

    private expanded = new BehaviorSubject<boolean>(false);

    get isExpanded() {
        return this.expanded.asObservable();
    }

    public setSidenav(sidenav: MatSidenav) {
        this.sidenav = sidenav;
    }

    public open() {
        this.expanded.next(true);
        // return this.sidenav.open();
    }

    public close() {
        this.expanded.next(false);
        // return this.sidenav.close();
    }

    public toggle() {
        this.expanded.next(!this.expanded.value);
        // this.sidenav.toggle();
    }
}
