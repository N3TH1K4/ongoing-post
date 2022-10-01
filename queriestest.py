
anime_query = '''
   query ($id: Int,$page: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
            month
            day
          }
        endDate{
            year
            month
            day
            }
          episodes
          isLicensed
          recommendations(page:$page, perPage:10, sort:RATING_DESC,){
            pageInfo {
                lastPage
                total}
            edges{
                node{
                    mediaRecommendation{title{romaji}
                    coverImage{
              extraLarge}
              siteUrl
              averageScore
                    id}
                    rating
                }}
          }
          isAdult
          popularity
          source
          externalLinks{
              type
              url
              site
              language
              icon
              isDisabled
              }
          season
          type
          format
          status
          countryOfOrigin
          duration
          hashtag
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          nextAiringEpisode {
              timeUntilAiring
              episode
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          synonyms
          relations{
            edges{
                relationType
                node{
                    title{romaji}}
                    }
          }
          bannerImage
          coverImage{
              extraLarge}
          characters(page: $page, perPage: 25,sort:ROLE){
                pageInfo {
                    lastPage
                    total
              }
              edges{
                  node{
                    name{full}
                      }
                  role
                  }
                }
                  
      }
    }
'''


animeb= """
query ($id: Int,$page: Int,$search: String) { 
      Media (id: $id, type: ANIME{
        bannerImage
      }}

"""
