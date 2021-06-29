import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-historical-dashboard',
  templateUrl: './historical-dashboard.component.html',
  styleUrls: ['./historical-dashboard.component.scss'],
})
export class HistoricalDashboardComponent implements OnInit {


  public environmentDashboard: any = 'http://your_ip/app/dashboards#'; // Copy here the dashboard URL from your Kibana  
  

  public fireDashboard: any = 'http://your_ip/app/dashboards#'; // Copy here the dashboard URL from your Kibana
  public dashboardRef: any;

  constructor(private sanitizer: DomSanitizer) {
    this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.environmentDashboard);
   }


  public ngOnInit(): void {
  }
  public changeDashboard(dashboard: string): void {
    switch (dashboard) {
      case 'environment':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.environmentDashboard);
        break;
      case 'fire':
        this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.fireDashboard);
        break;
    }
  }

}
