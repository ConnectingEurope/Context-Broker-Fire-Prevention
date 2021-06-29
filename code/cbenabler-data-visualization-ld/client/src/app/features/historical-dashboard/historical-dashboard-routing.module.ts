import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HistoricalDashboardComponent } from './components/historical-dashboard.component';

const routes: Routes = [{ path: '', component: HistoricalDashboardComponent }];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class HistoricalDashboardRoutingModule { }
