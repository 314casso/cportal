import { Component, OnInit } from '@angular/core';
import { MenuItems } from './menu-items';

import { Observable } from 'rxjs/Observable';

import { SidenavService } from '../../_services/sidenav.service';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.css']
})
export class SidenavComponent implements OnInit {
  public menuItems: Array<Object>;
  isExpanded$: Observable<boolean>;

  constructor(
    private sidenav: SidenavService
  ) { }

  ngOnInit(): void {
    this.menuItems = MenuItems;
    this.isExpanded$ = this.sidenav.isExpanded;
  }
}
