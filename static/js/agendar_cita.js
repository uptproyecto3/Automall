

//Esta funcion llama a un selector de hora para que exista uno tambien en navegadores firefox
flatpickr("#hora_cita", {
                                    locale:"es",
                                    enableTime: true,
                                    noCalendar: true,
                                    dateFormat: "H:i:S",  // Formato 24h ideal para que MySQL lo entienda directo (Ej: 15:30)
                                    time_24hr: true,
                                    minuteIncrement: 30,
                                    minTime:"8:00",
                                    maxTime:"18:00"                               
                                 });