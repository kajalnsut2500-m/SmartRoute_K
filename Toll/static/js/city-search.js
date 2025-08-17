document.querySelectorAll('.city-search').forEach(input => {
   /* input.addEventListener('input', async function() {
        if(this.value.length < 3) return;
        
        const response = await fetch(`/api/city-search?q=${encodeURIComponent(this.value)}`);
        const cities = await response.json();
        
        const datalist = document.getElementById(`${this.id}-cities`);
        datalist.innerHTML = '';
        
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            datalist.appendChild(option);
        });
    });*/
    input.addEventListener('input', function() {
        if(this.value.length < 2) return;
        
        fetch(`/api/city-search?q=${encodeURIComponent(this.value)}`)
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(data => {
                const datalist = document.querySelector(`#${this.getAttribute('list')}`);
                if (datalist) {
                    datalist.innerHTML = '';
                    data.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city;
                        datalist.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('City search failed:', error);
            });
    });

});