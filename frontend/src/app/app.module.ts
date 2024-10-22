import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { EventListComponent } from './event-list/event-list.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    EventListComponent  // Déclare ton composant ici
  ],
  imports: [
    BrowserModule,       // Utilise BrowserModule pour l'application Angular principale
    HttpClientModule,    // Module pour faire des requêtes HTTP
    AppComponent         // Import the standalone component here
  ],
  providers: [],
  bootstrap: []
})
export class AppModule { }
