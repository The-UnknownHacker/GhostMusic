const app = Vue.createApp({
    data() {
        return {
            prompt: '',
            isProcessing: false,
            audioFileUrl: null
        };
    },
    methods: {
        async onSubmit() {
            if (this.prompt.trim() === '') return;
            this.isProcessing = true;

            const formData = new FormData();
            formData.append('prompt', this.prompt);

            try {
                const response = await fetch('/generate_audio', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const audioUrl = URL.createObjectURL(blob);
                    this.audioFileUrl = audioUrl;
                } else {
                    alert('Error generating audio. Please try again.');
                }
            } catch (error) {
                console.error(error);
                alert('Something went wrong. Please try again.');
            } finally {
                this.isProcessing = false;
            }
        }
    }
});

app.mount('#app');
