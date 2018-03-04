import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from './_guards/auth.guard';

import { HomeLayoutComponent } from './layout/home-layout/home-layout.component';
import { LoginLayoutComponent } from './layout/login-layout/login-layout.component';

import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SupportComponent } from './support/support.component';
import { InfoComponent } from './info/info.component';
import { SettlementComponent } from './settlement/settlement.component';
import { TrackingComponent } from './tracking/tracking.component';

const appRoutes: Routes = [
  {
    path: '', component: HomeLayoutComponent, canActivate: [AuthGuard], children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' },
      { path: 'home', component: HomeComponent },
      { path: 'support', component: SupportComponent },
      { path: 'info', component: InfoComponent },
      { path: 'settlement', component: SettlementComponent },
      { path: 'tracking', component: TrackingComponent },
    ]
  },
  {
    path: '', component: LoginLayoutComponent, children: [
      { path: 'login', component: LoginComponent }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }
