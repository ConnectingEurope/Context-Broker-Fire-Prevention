import { Component, OnInit, ViewChild } from '@angular/core';
import { MenuItem } from 'primeng/api/menuitem';
import { OverlayPanel } from 'primeng/overlaypanel/public_api';
import { Router } from '@angular/router';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {

    public menuItems: MenuItem[];
    public notificationsCount: number = 4;
    public logged: boolean = false;
    @ViewChild('notificationsPanel') private notificationPanel: OverlayPanel;
    // @ViewChild('layerPanel') private layerPanel: OverlayPanel;

    constructor( private router: Router){}
    public ngOnInit(): void {
        // const logged = localStorage.getItem('logged');
        // if(logged ==='true'){
        //     this.logged = true;
        // }else{
        //     this.logged = false;
        // }
        this.logged = sessionStorage.getItem('logged') === 'true';
        this.loadMenu();
    }

    public onNotificationsClick(event: any): void {
        this.router.navigate(["/notifications"]);
    }

    private loadMenu(): void {
        this.menuItems = [
            { label: 'Map', icon: 'fas fa-globe-europe', routerLink: '/map' },
            { label: 'Historical', icon: 'fas fa-chart-area', routerLink: '/dashboard' },
            { label: 'Configuration', icon: 'fas fa-cog', routerLink: '/configuration', visible: this.logged },
            { label: 'Rules', icon: 'fas fa-database', routerLink: '/rule-engine',visible: this.logged },
        ];
    }
    onLoginClick(){
        this.router.navigate(["/signin"]);
    }
    onCreateUserClick(){
        this.router.navigate(["/signup"]);
    }
    onLogoutClick(){
        sessionStorage.setItem("logged","false");
        sessionStorage.removeItem("userData")
        this.router.navigate(["/"]).then(() => {
            window.location.reload();
          });
    }
}
