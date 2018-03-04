import { Component, OnInit } from '@angular/core';
import { SidenavService } from '../../_services/sidenav.service';
import { AuthenticationService } from '../../_services/authentication.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {
  isLoggedIn$: Observable<boolean>;

  constructor(
    private authService: AuthenticationService,
    private sidenav: SidenavService
  ) { }

  ngOnInit() {
    this.isLoggedIn$ = this.authService.isLoggedIn;
  }

  onLogout() {
    this.authService.logout();
  }
}
