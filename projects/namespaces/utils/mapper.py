def from_projects_to_projectDtos(projects):
        projects_images =[]
        for project in projects:
            url_images = []
            for image in project['images']:
                url_images.append(image['url'])
            project['images'] = url_images
            projects_images.append(project)
        projects_final = []
        for project in projects_images:
            url_videos = []
            for video in project['videos']:
                url_videos.append(video['url'])
            project['videos'] = url_videos
            projects_final.append(project) 
        return projects_final   
