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
			var resource = this.$resource(this.apiUrl)
			resource.get().then(
				(response) => 
				{
					this.transportArrivalList = response.data
				})
		},
	},
	data:
	{
		apiUrl: '/api/get',
		transportArrivalList: [],
	},
});
