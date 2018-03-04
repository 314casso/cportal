import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthenticationService } from '../_services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  private formSubmitAttempt: boolean;
  private errorOccured: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private authenticationService: AuthenticationService
  ) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      userName: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  isFieldInvalid(field: string) {
    return (!this.form.get(field).valid && this.form.get(field).touched) || (this.form.get(field).untouched && this.formSubmitAttempt);
  }

  onSubmit() {
    if (this.form.valid) {
      this.authenticationService.login(this.form.value)
                                .subscribe(result => this.errorOccured = !result);
    }
    this.formSubmitAttempt = true;
  }
}
