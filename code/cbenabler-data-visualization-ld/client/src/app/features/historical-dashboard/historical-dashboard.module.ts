import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HistoricalDashboardRoutingModule } from './historical-dashboard-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { CardModule } from 'primeng/card/';
import { CalendarModule } from 'primeng/calendar';
import { FormsModule } from '@angular/forms';
import { ProgressBarModule } from 'primeng/progressbar';
import { DialogModule } from 'primeng/dialog';
import { HistoricalDashboardComponent } from './components/historical-dashboard.component';


@NgModule({
    declarations: [
        HistoricalDashboardComponent,
    ],
    imports: [
        CommonModule,
        SharedModule,
        CardModule,
        HistoricalDashboardRoutingModule,
        FormsModule,
        CalendarModule,
        ProgressBarModule,
        DialogModule,
    ],
})
export class HistoricalDashboardModule { }
