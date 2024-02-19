######################################################################
###
###		Studentas
###			vardas: Agnė
###			pavarde: Židanavičiūtė
###
#######################################################################
### 		Viso galima surinkti 19 taškų. 19 t = 10 balų. 			###
#######################################################################

/* 
*	UŽDUOTIS 01: 
*	(1 taškas)
*	Pateikite tik tuos mokėjimus, kurių vertė (amount) yra didesnė nei 2. 
*   Naudokite lentelę payment.
*/
	
		select
			distinct amount
		from sakila.payment
        where amount > 2;
    
/* 
*	UŽDUOTIS 02: 
*	(1 taškas)
*	Pateikite filmus, kurių reitingas (rating) yra „PG“,
*	o pakeitimo kaina (replacement_cost) yra mažesnė nei 10. 
*    Naudokite lentelę film.
*/
	
		select
			title,
            rating,
            replacement_cost
		from sakila.film
        where rating = 'pg' and replacement_cost < 10;
    
/* 
*	UŽDUOTIS 03: 
*	(1 taškas)
*	Suskaičiuokite vidutinę nuomos kainą (rental_rate) kiekvieno
*	reitingo filmams, atsakymą pateikite tik su 2 skaičiais po kablelio. 
*   Ne apvalinti! Tiesiog „nupjauti“ atsakymą ties dviem skaičiais po kablelio. 
*	Naudokite lentelę film.
*/
	
		select
			rating,
            truncate(avg(rental_rate),2) 'average_rental_rate'
		from sakila.film
        group by rating;
    
/* 
*	UŽDUOTIS 04: 
*	(1 taškas)
*	Išspausdinkite visų klientų vardus (first_name), o šalia vardų stulpelio
*	suskaičiuokite kiekvieno vardo ilgį (kiek varde yra raidžių). 
*	Naudokite lentelę customer
*/
	
    select
		distinct first_name,
        length(first_name) 'vardo ilgis'
	from sakila.customer;
    
/* 
*	UŽDUOTIS 05: 
*	(1 taškas)
*	Ištirkite kelinta raidė yra „e“ kiekvieno filmo aprašyme (description).
*	Naudokite lentelę film.
*/    
    
		select
			description,
            locate('e', description) 'e raides lokacija'
		from sakila.film;
    
/* 
*	UŽDUOTIS 06: 
*	(2 taškai)
*	Susumuokite kiekvieno reitingo (rating) bendrą filmų trukmę (length).
*	Išspausdinkite tik tuos reitingus, kurių bendra filmų trukmė yra
*	ilgesnė nei 22000.
*	Naudokite lentelę film.
*/   
	
		select
			rating,
            sum(length) 'bendra filmu trukme'
        from sakila.film
        group by rating
        having sum(length) > 22000;
    
/* 
*	UŽDUOTIS 07: 
*	(2 taškai)
*	Išspausdinkite visų filmų aprašymus (description), šalia išspausdinkite
*	aprašymus sudarančių elementų skaičių. Trečiame stulpelyje išspausdinkite
*	aprašymų elemetnų skaičių, juose visas raides „a“ pakeisdami į „OO“.
*	Tai reiškia turite aprašyme visas raides „a“ pakeisti į „OO“ ir tada
*	suskaičiuoti naujo objekto elementų skaičių. 
*	Naudokite lentelę film_text.
*/ 
	
		select
			description,
            length(description) 'elementu skaicius',
            modified_description, length(modified_description) 'naujas elementu skaicius'
		from
        (select description, replace(description, 'a', 'OO')modified_description from sakila.film_text) x;
            

/* 
*	UŽDUOTIS 08: 
*	(3 taškai)
*	Parašykite SQL užklausą, kuri suskirstytų filmus pagal jų reitingus (rating)
*	į tokias kategorijas:
*		Jei reitingas yra „PG“ arba „G“ tada „PG_G“
*		Jei reitingas yra „NC-17“ arba „PG-13“ tada „NC-17-PG-13“
*		Visus kitus reitingus priskirkite kategorijai „Nesvarbu“
*	Kategorijas atvaizduokite stulpelyje „Reitingo_grupe“
*	Naudokite lentelę film.
*/ 
	
		select distinct rating,
			case
				when rating = 'PG' or rating = 'G' then 'PG_G'
                when rating = 'NC-17' or rating = 'PG-13' then 'NC-17-PG-13'
                else 'Nesvarbu'
			end Reitingo_grupe
		from sakila.film;
    
/* 
*	UŽDUOTIS 09: 
*	(3 taškai)
*	Susumuokite nuomavimosi trukmę (rental_duration), kiekvienanai filmo
*	kategorijai (name). 
*	Išspausdinkite tik tas kategorijos, kurių rental_duration suma yra 
*	didesnė nei 300. 
*	Užduotį atlikite apjungiant lenteles. 
*	Naudokite lenteles film, film_category, category.
*/ 
	
		select
			c.name,
			sum(f.rental_duration) 'Nuomos trukmes suma'
		from sakila.category c
        join sakila.film_category fc on c.category_id = fc.category_id
        join sakila.film f on fc.film_id = f.film_id
        group by c.name
        having sum(f.rental_duration)>300;
            
    
/* 
*	UŽDUOTIS 10: 
*	(4 taškai su subquery, be subguery 2 taškai)
*	Pateikite klientų vardus (first_name) ir pavardes (last_name), kurie 
*	išsinuomavo filmą „AGENT TRUMAN“. Užduotį atlikite naudodami subquery.
*	Užduotis atlikta teisingai be subquery vertinama 2t. 
*	Naudokite lenteles customer, rental, inventory, film.
*/ 
	
    /*
    film       film_id
    customer   customer_id
    rental     customer_id, inventory_id
    inventory  inventory_id, film_id
    */
    
    
    #1 Budas
    
    select distinct first_name, last_name from sakila.customer 
		where customer_id in (
	select customer_id from sakila.rental 
		where inventory_id in (
	select inventory_id from sakila.inventory
		where film_id = (
	select film_id from sakila.film
		where title = 'AGENT TRUMAN'
		)));

  
    #2 Budas
    
    select 
		distinct c.first_name, c.last_name,
        f.title
    from sakila.customer c
    join sakila.rental r on c.customer_id = r.customer_id
    join sakila.inventory i on i.inventory_id = r.inventory_id
    join sakila.film f on f.film_id = i.film_id
    where f.title = 'AGENT TRUMAN'
    group by c.first_name, c.last_name;
    
    