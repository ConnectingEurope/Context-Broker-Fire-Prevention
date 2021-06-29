import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationsRoutingModule } from './notifications-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { CardModule } from 'primeng/card/';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule } from '@angular/forms';
import { ProgressBarModule } from 'primeng/progressbar';
import { DialogModule } from 'primeng/dialog';
import { NotificationsComponent } from './notifications.component';


@NgModule({
    declarations: [
        NotificationsComponent,
    ],
    imports: [
        CommonModule,
        SharedModule,
        CardModule,
        NotificationsRoutingModule,
        FormsModule,
        CalendarModule,
        ProgressBarModule,
        DialogModule,
    ],
})
export class NotificationsModule { }
