import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';

import { NewsService } from '../_services/news.service';
import { EmployeeService } from '../_services/employee.service';

import { News } from '../_models/news';
import { Employee } from '../_models/employee';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  news$: Subscription;
  employee$: Subscription;

  news: News[];
  employee: Employee;
  head: Employee;

  constructor(
    private newsService: NewsService,
    private employeeService: EmployeeService
  ) { }

  ngOnInit() {
    this.employee$ = this.employeeService.getEmployees().subscribe(result => {
      this.employee = result[0];
      this.head = this.employee.head;
    });

    this.news$ = this.newsService.getNews().subscribe(result => {
      this.news = result;
    });
  }

  ngOnDestroy() {
    this.news$.unsubscribe();
    this.employee$.unsubscribe();
  }
}
