import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SigninPageRoutingModule } from './siginin-page-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { CardModule } from 'primeng/card/';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { ProgressBarModule } from 'primeng/progressbar';
import { DialogModule } from 'primeng/dialog';
import { SigninPageComponent } from './signin-page.component';

@NgModule({
  declarations: [
    SigninPageComponent
  ],
  imports: [
    CommonModule,
        SharedModule,
        CardModule,
        SigninPageRoutingModule,
        FormsModule,
        CalendarModule,
        ProgressBarModule,
        DialogModule,
        FormsModule,
        ReactiveFormsModule,
  ]
})
export class SigninPageModule { }
