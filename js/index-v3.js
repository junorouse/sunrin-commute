var main = new Vue({
	el: '#app',
	mounted: function()
	{
		this.getTransportArrivalList();
		setInterval(function(){main.getTransportArrivalList()}, 5000);
	},
	methods:
	{
		getTransportArrivalList: function()
		{
			var reloadBtn = document.getElementById("reload_btn");
			reloadBtn.innerText = "새로고침 중 ... ";
			var resource = this.$resource(this.apiUrl)
			resource.get().then(
				(response) => 
				{
					this.transportArrivalList = response.data
					reloadBtn.innerText = "새로고침";
				});
		},
	},
	data:
	{
		apiUrl: '/api/get',
		transportArrivalList: [],
	},
});

