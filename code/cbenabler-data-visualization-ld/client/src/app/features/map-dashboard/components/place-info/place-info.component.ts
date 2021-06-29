import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { takeUntil } from 'rxjs/operators';
import { BaseComponent } from 'src/app/shared/misc/base.component';
import { Entity } from 'src/app/shared/models/entity';
import { ModelDto } from 'src/app/shared/models/model-dto';
import { MapDashboardService } from '../../services/map-dashboard.service';

@Component({
  selector: 'app-place-info',
  templateUrl: './place-info.component.html',
  styleUrls: ['./place-info.component.scss'],
})
export class PlaceInfoComponent  implements OnInit{

  private firstLoad: boolean = false;
  smokeEntity: Entity;
  forestEntity: Entity;
  fireEntity: Entity;

  constructor( private mapDashBoardService: MapDashboardService) {

    this.mapDashBoardService.getEntitiesData(!this.firstLoad).toPromise().then(
      (models: ModelDto[]) => {
        models.forEach((model, i) => {
          model.data.forEach(entity =>{
            console.log("entities: " + entity.id);
             switch(entity.id){
              case 'urn:ngsi-ld:FireForestStatus:Ourense:FFS001':
                this.fireEntity = entity;
                console.log(this.fireEntity);
                break;
              case 'urn:ngsi-ld:FireForestStatus:Ourense:FFS002':
                this.smokeEntity = entity;
                console.log(this.smokeEntity);
                break;
              case 'urn:ngsi-ld:FireForestStatus:Ourense:FFS003':
                this.forestEntity = entity;
                console.log(this.forestEntity);
                break;  
             }
          });
         
      });
      });
   }

  public ngOnInit(): void {

  }

}
