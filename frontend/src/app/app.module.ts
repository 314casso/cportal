import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { PathLocationStrategy, LocationStrategy } from '@angular/common';

import { registerLocaleData } from '@angular/common';
import localeRu from '@angular/common/locales/ru';
registerLocaleData(localeRu);

import { MaterialModule } from './shared/material.module';
import { AppRoutingModule } from './app-routing.module';

import { AuthGuard } from './_guards/auth.guard';

import { AuthenticationService } from './_services/authentication.service';
import { AuthInterceptor } from './_interceptors/auth.interceptor';

import { SidenavService } from './_services/sidenav.service';
import { NewsService } from './_services/news.service';
import { EmployeeService } from './_services/employee.service';
import { TrackingService } from './_services/tracking.service';

import { AppComponent } from './app.component';
import { HomeLayoutComponent } from './layout/home-layout/home-layout.component';
import { LoginLayoutComponent } from './layout/login-layout/login-layout.component';
import { SidenavComponent } from './layout/sidenav/sidenav.component';
import { ToolbarComponent } from './layout/toolbar/toolbar.component';
import { FooterComponent } from './layout/footer/footer.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { SettlementComponent } from './settlement/settlement.component';
import { TrackingComponent } from './tracking/tracking.component';
import { SupportComponent } from './support/support.component';
import { InfoComponent } from './info/info.component';

@NgModule({
  declarations: [
    AppComponent,
    SidenavComponent,
    ToolbarComponent,
    FooterComponent,
    HomeLayoutComponent,
    LoginLayoutComponent,
    HomeComponent,
    SupportComponent,
    InfoComponent,
    LoginComponent,
    SettlementComponent,
    TrackingComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    MaterialModule,
    AppRoutingModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true, },
    AuthGuard,
    AuthenticationService,
    SidenavService,
    NewsService,
    EmployeeService,
    TrackingService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
