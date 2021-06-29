import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.scss'],
})
export class NotificationsComponent implements OnInit {

  public notifications: any = 'http://46.17.108.68:5601/app/dashboards#/view/75e68220-b22f-11eb-9713-7da4e26b458c?embed=true'+
  '&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-7d%2Cto%3Anow))&show-time-filter=true&hide-filter-bar=true';
  public dashboardRef: any;
  
  constructor(private sanitizer: DomSanitizer) {
    this.dashboardRef = this.sanitizer.bypassSecurityTrustResourceUrl(this.notifications);
   }
  
  public ngOnInit(): void {
  }

}
