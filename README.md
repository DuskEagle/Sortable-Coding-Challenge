# Sortable Coding Challenge

The goal of this project is to match a set of product listings against a set of known products, taking care not to incorrectly match any listings. The full details can be found at [http://sortable.com/challenge](http://sortable.com/challenge).

## Running The Code

Tested with Python 3.3, though any version of Python 3 should work.

    cd src
    python3 ProductListingMatcher.py

A file named "results.txt" will be created in the data directory containing the results of the program.
    
You can also pass the program three command line arguments specifying alternate products, listings, and results files, like so:

    python3 ProductListingMatcher.py products-file listings-file results-file`

## How It Works

The basic idea behind this approach is that a listing is matched with a product if and only if the product manufacturer and model appear in the listing title, and exactly one product is matched with the listing. From this idea, we apply several refinements to improve the amount of matches and eliminate false positives.

The very first thing we do after reading in a product or a listing is to "normalize" the fields we will be matching for. At the very least, this involves converting all the text fields to lower case. We also strip the manufacturer name down to the "root" name, so that e.g. "Canon" and "Canon Canada" will both be matched as the same manufacturer. A special case is used to handle HP, which could be listed as HP or Hewlett Packard.

We use a dictionary to store mappings from pairs of (manufacturer, model names) to sets of products. This enables [average case O(1) lookup](https://wiki.python.org/moin/TimeComplexity) for any product in the dictionary. The vast majority of products are uniquely identified by the manufacurer and model name pair, but there are a couple of products which share the same manufacturer and model name. We'll talk about those after.

For most listings, it is necessary and sufficient that we find exactly one product that has the same manufacturer as given in the listing, and whose model appears within the listing. However, there could be subtle differences between the model name as listed in products.txt and the way the listings list the model. For example, products.txt might give the model name as "QV 3000EX", whereas in a listing the model is given as "QV3000 EX". Other problems that can arise are that we are checking a listing for model "700", but the listing is actually for a model "7000" device.

To handle all of these issues, we build a custom regular expression pattern for each product model name, which allows for spaces or hyphens between characters in the model name and also ensures that model names which are prefixes of other model names do not match return results for the former when the listing is actually for the latter. So our dictionary from before is actually a map from (manufacturer, model_name_regex) pairs to sets of products, and the regex pattern gets applied to each listing to detect a potential match.

We mentioned above that there are a small amount of products which share the same manufacturer and model. If a listing has been matched with one of these products, we also search the listing for the product family name as well. As before, exactly one product can be a match, otherwise we don't match the listing with any product.

One of the points emphasized quite heavily in the challenge is that it is very important to avoid false positives in matching listings to products. I found that the policy of discarding any listing which matched more than one potential product was very helpful in eliminating most false positives from the results. Many of the listings that had the potential to be confused as a wrong product were for various accessories related to the product. These listings usually listed many different models they were compatible with, which made it easy to not match them to any product. 

This filtered out the vast majority of the false positives, but there were still a very small amount that slipped through. From looking at the remaining cases, they were all of the form "<Accessory> for <model(s)>". So, I decided to filter out everything in a listing after the first instance of the word "for". We also check for the word "for" in a few other languages, as not all of the listings are in English. 
