import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CanActivateGuard } from './shared/services/guard.service';

const routes: Routes = [
    {
        path: 'map',
        loadChildren: (): any => import('./features/map-dashboard/map-dashboard.module').then(m => m.MapDashboardModule),
        canActivate: [CanActivateGuard]
        
    },
    {
        path: 'configuration',
        loadChildren: (): any => import('./features/config-dashboard/config-dashboard.module').then(m => m.ConfigDashboardModule),
        canActivate: [CanActivateGuard]
    },
    {
        path: 'dashboard',
        loadChildren: (): any => import('./features/historical-dashboard/historical-dashboard.module')
        .then(m => m.HistoricalDashboardModule),
    },
    {
        path: 'signin',
        loadChildren: (): any => import('./features/signin-page/signin-page.module')
        .then(m => m.SigninPageModule),
    },
    {
        path: 'signup',
        loadChildren: (): any => import('./features/signup-page/signup-page.module')
        .then(m => m.SignupPageModule),
        canActivate: [CanActivateGuard]
    },
    {
        path: 'notifications',
        loadChildren: (): any => import('./features/notifications/notifications.module')
        .then(m => m.NotificationsModule),
        canActivate: [CanActivateGuard]
    },
    {
        path: 'historical-data/:type/:id',
        loadChildren: (): any => import('./features/historical-data/historical-data.module').then(m => m.HistoricalDataModule),
        canActivate: [CanActivateGuard]
    },
    {
        path: 'rule-engine',
        loadChildren: (): any => import('./features/rule-dashboard/rule-dashboard.module').then(m => m.RuleDashboardModule),
        canActivate: [CanActivateGuard]
    },
    {
        path: '',
        redirectTo: 'map',
        pathMatch: 'full',
        canActivate: [CanActivateGuard]
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
    exports: [RouterModule],
})
export class AppRoutingModule { }
