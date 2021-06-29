import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CanActivate } from '@angular/router';
import { LoginService } from './login.service';

@Injectable()
export class CanActivateGuard implements CanActivate{

  constructor( private router: Router, private authService: LoginService) { }
  canActivate(){
    if(!this.authService.isLogged()){
      console.log("You are not logged");
      this.router.navigate(["/signin"]);
      return false;
    }
    return true;
  }
}
