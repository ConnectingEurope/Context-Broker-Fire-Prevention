import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SignupPageRoutingModule } from './siginup-page-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { CardModule } from 'primeng/card/';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { ProgressBarModule } from 'primeng/progressbar';
import { DialogModule } from 'primeng/dialog';
import { SignupPageComponent } from './signup-page.component';

@NgModule({
  declarations: [
    SignupPageComponent
  ],
  imports: [
    CommonModule,
        SharedModule,
        CardModule,
        SignupPageRoutingModule,
        FormsModule,
        ReactiveFormsModule,
        CalendarModule,
        ProgressBarModule,
        DialogModule,
  ]
})
export class SignupPageModule { }
