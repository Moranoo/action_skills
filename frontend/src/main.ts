import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app/app-routing.module';  // Importation des routes

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),  // Fournir HttpClient pour les requêtes HTTP
    provideRouter(routes)  // Fournir le routeur avec les routes
  ]
}).catch(err => console.error(err));
