import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from  '../models/user';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  // private base_url: string = 'http://46.17.108.68:5000/'
  private base_url: string = '/api'
  private user_route: string = '/user'
  private logged: boolean = false;
  constructor(private http: HttpClient) { }

  isLogged(){
    // let isLogged = localStorage.getItem('logged');
    // if(isLogged ==='true'){
    //   this.logged = true;
    // }else{
    //   this.logged = false;
    // }
    // return this.logged;
    return sessionStorage.getItem('logged') === 'true';
  }

  setSessionStorage(logged){
    sessionStorage.setItem('logged', logged);
  }

  login(user: User){
    user.register = false;
    const loggedUser = this.http.post<User>(this.base_url + this.user_route, user);
    return loggedUser;
  }
  register(user: User){
    user.register = true;
    const idNewUSer = this.http.post<number>(this.base_url + this.user_route, user);
    return idNewUSer;
  }

  
}
