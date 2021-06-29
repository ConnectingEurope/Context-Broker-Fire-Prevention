import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RuleDashboardComponent } from './components/rule-dashboard.component';

const routes: Routes = [{ path: '', component: RuleDashboardComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RuleDashboardRoutingModule { }
